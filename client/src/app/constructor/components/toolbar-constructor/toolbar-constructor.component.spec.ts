import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToolbarConstructorComponent } from './toolbar-constructor.component';

describe('ToolbarConstructorComponent', () => {
  let component: ToolbarConstructorComponent;
  let fixture: ComponentFixture<ToolbarConstructorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToolbarConstructorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToolbarConstructorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
